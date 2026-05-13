from collections import defaultdict
import locale
from app.models.department import Department
from app.models.user import User
from app.models.schedule import Schedule
from app.schemas.schedules import DepartamentoEscala, DiaEscala, MembroEquipe
from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

# Mapeamento de dia da semana (0=segunda, 6=domingo)
DIAS_SEMANA = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo",
}

# Mapeamento de meses em português
MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}


def _formatar_data(dt) -> str:
    """Formata datetime para '04 de Maio'."""
    dia = dt.day
    mes = MESES_PT.get(dt.month, "")
    return f"{dia:02d} de {mes}"


def _formatar_dia_semana(dt) -> str:
    """Formata datetime para 'Domingo — 19h'."""
    dia_semana = DIAS_SEMANA.get(dt.weekday(), "")
    hora = dt.strftime("%Hh")
    return f"{dia_semana} — {hora}"


def _calcular_status(departamentos_escala: list, todos_departamentos: list) -> str:
    """
    Calcula o status da escala de um dia:
    - 'critica': nenhum departamento tem voluntários
    - 'alerta': algum departamento ficou sem voluntários
    - 'confirmada': todos os departamentos têm ao menos 1 voluntário
    """
    ids_com_equipe = {d["id"] for d in departamentos_escala if len(d["equipe"]) > 0}
    ids_todos = {d.id for d in todos_departamentos}

    if len(ids_com_equipe) == 0:
        return "critica"
    elif ids_com_equipe < ids_todos:
        return "alerta"
    else:
        return "confirmada"


async def get_monthly_schedules(session: AsyncSession, mes: int, ano: int) -> list[DiaEscala]:
    """
    Busca todas as escalas do mês/ano e retorna agrupadas:
    Dia → Departamentos → Equipe (profissionais)
    """
    try:
        # 1. Buscar todos os departamentos do sistema
        dept_result = await session.execute(select(Department))
        todos_departamentos = dept_result.scalars().all()

        # 2. Query principal: Schedule + User + Department via JOINs
        query = (
            select(Schedule, User, Department)
            .join(User, Schedule.user_id == User.id)
            .join(Department, Schedule.department_id == Department.id)
            .where(
                extract('month', Schedule.data_hora) == mes,
                extract('year', Schedule.data_hora) == ano,
            )
            .order_by(Schedule.data_hora)
        )

        resultado = await session.execute(query)
        rows = resultado.all()

        # 3. Agrupar por data (dia) → departamento → membros
        # Estrutura: { "2026-05-04": { dept_id: { "nome": "...", "membros": [...] } } }
        agrupado_por_dia = defaultdict(lambda: defaultdict(lambda: {"nome": "", "membros": []}))
        datas_originais = {}  # Guarda o datetime original para formatação

        for schedule, user, department in rows:
            date_key = schedule.data_hora.date().isoformat()

            # Guarda a primeira ocorrência do datetime para formatação
            if date_key not in datas_originais:
                datas_originais[date_key] = schedule.data_hora

            dept_group = agrupado_por_dia[date_key][department.id]
            dept_group["nome"] = department.nome

            # Evita duplicatas (mesmo user pode ter apenas 1 escala por dept/dia)
            ids_existentes = {m["id"] for m in dept_group["membros"]}
            if user.id not in ids_existentes:
                dept_group["membros"].append({"id": user.id, "nome": user.nome})

        # 4. Montar resposta hierárquica
        resposta: list[DiaEscala] = []

        for date_key in sorted(agrupado_por_dia.keys()):
            dt_original = datas_originais[date_key]
            departamentos_lista = []

            for dept_id, dept_data in agrupado_por_dia[date_key].items():
                departamentos_lista.append({
                    "id": dept_id,
                    "nome": dept_data["nome"],
                    "equipe": dept_data["membros"],
                    "alerta": None,
                })

            # Verificar departamentos sem voluntários neste dia
            ids_presentes = set(agrupado_por_dia[date_key].keys())
            for dept in todos_departamentos:
                if dept.id not in ids_presentes:
                    departamentos_lista.append({
                        "id": dept.id,
                        "nome": dept.nome,
                        "equipe": [],
                        "alerta": "Sem voluntários escalados",
                    })

            status = _calcular_status(departamentos_lista, todos_departamentos)

            resposta.append(DiaEscala(
                dia=date_key,
                dia_formatado=_formatar_data(dt_original),
                dia_semana=_formatar_dia_semana(dt_original),
                status=status,
                departamentos=departamentos_lista,
            ))

        return resposta

    except Exception as e:
        raise e