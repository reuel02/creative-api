-- Inserindo Departamentos
INSERT INTO departamentos (id, nome) VALUES
(1, 'Mídia'),
(2, 'Corte de Câmera'),
(3, 'Iluminação'),
(4, 'Som'),
(5, 'Transmissão')
ON CONFLICT (id) DO NOTHING;

-- Atualizando a sequência de departamentos
SELECT setval('departamentos_id_seq', (SELECT MAX(id) FROM departamentos));

-- Inserindo Usuários (Voluntários)
INSERT INTO usuarios (id, nome, telefone, department_id, email, cargo, ativo, data_entrada) VALUES
(1, 'João Silva', '11999999991', 1, 'joao.silva@email.com', 'Líder', true, '2023-01-15 10:00:00'),
(2, 'Maria Oliveira', '11999999992', 1, 'maria.oliveira@email.com', 'Voluntário', true, '2023-03-20 10:00:00'),
(3, 'Pedro Santos', '11999999993', 2, 'pedro.santos@email.com', 'Líder', true, '2023-02-10 10:00:00'),
(4, 'Ana Costa', '11999999994', 2, 'ana.costa@email.com', 'Voluntário', true, '2023-05-05 10:00:00'),
(5, 'Lucas Pereira', '11999999995', 3, 'lucas.pereira@email.com', 'Líder', true, '2023-01-20 10:00:00'),
(6, 'Julia Rodrigues', '11999999996', 3, 'julia.rodrigues@email.com', 'Voluntário', false, '2023-06-15 10:00:00'),
(7, 'Marcos Souza', '11999999997', 4, 'marcos.souza@email.com', 'Líder', true, '2023-04-10 10:00:00'),
(8, 'Carla Lima', '11999999998', 4, 'carla.lima@email.com', 'Voluntário', true, '2023-07-22 10:00:00'),
(9, 'Roberto Alves', '11999999999', 5, 'roberto.alves@email.com', 'Líder', true, '2023-02-28 10:00:00'),
(10, 'Fernanda Gomes', '11999999910', 5, 'fernanda.gomes@email.com', 'Voluntário', true, '2023-08-14 10:00:00')
ON CONFLICT (id) DO NOTHING;

-- Atualizando a sequência de usuários
SELECT setval('usuarios_id_seq', (SELECT MAX(id) FROM usuarios));

-- Inserindo Cultos (Usando o mês atual/próximos)
INSERT INTO cultos (id, nome, data) VALUES
(1, 'Culto de Domingo - Manhã', '2024-05-19 10:00:00'),
(2, 'Culto de Domingo - Noite', '2024-05-19 19:00:00'),
(3, 'Culto de Ensino', '2024-05-22 20:00:00'),
(4, 'Culto de Jovens', '2024-05-25 19:30:00')
ON CONFLICT (id) DO NOTHING;

-- Atualizando a sequência de cultos
SELECT setval('cultos_id_seq', (SELECT MAX(id) FROM cultos));

-- Inserindo Escalas
INSERT INTO escalas (id, user_id, department_id, culto_id, data_hora, observacoes) VALUES
(1, 1, 1, 1, '2024-05-19 10:00:00', 'Chegar 30 min mais cedo para testes'),
(2, 3, 2, 1, '2024-05-19 10:00:00', NULL),
(3, 5, 3, 1, '2024-05-19 10:00:00', NULL),
(4, 7, 4, 1, '2024-05-19 10:00:00', NULL),
(5, 9, 5, 1, '2024-05-19 10:00:00', NULL),

(6, 2, 1, 2, '2024-05-19 19:00:00', NULL),
(7, 4, 2, 2, '2024-05-19 19:00:00', 'Foco na transmissão ao vivo'),
(8, 8, 4, 2, '2024-05-19 19:00:00', NULL),
(9, 10, 5, 2, '2024-05-19 19:00:00', NULL),

(10, 1, 1, 3, '2024-05-22 20:00:00', NULL),
(11, 3, 2, 3, '2024-05-22 20:00:00', NULL),
(12, 7, 4, 3, '2024-05-22 20:00:00', NULL)
ON CONFLICT (id) DO NOTHING;

-- Atualizando a sequência de escalas
SELECT setval('escalas_id_seq', (SELECT MAX(id) FROM escalas));
