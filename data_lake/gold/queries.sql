-- =====================================
-- 1. Receita total por região
-- Pergunta: Qual região gera mais receita?
-- =====================================
SELECT 
    dl.borough,
    SUM(ft.total_amount) AS total_revenue
FROM fact_trips ft
JOIN dim_location dl 
    ON ft.pulocationid = dl.locationid
GROUP BY dl.borough
ORDER BY total_revenue DESC;


-- =====================================
-- 2. Distância média das corridas
-- Pergunta: Qual a distância média?
-- =====================================
SELECT 
    AVG(trip_distance) AS avg_distance
FROM fact_trips;


-- =====================================
-- 3. Corridas por tipo de pagamento
-- Pergunta: Como os clientes pagam?
-- =====================================
SELECT 
    payment_type,
    COUNT(*) AS total_trips
FROM fact_trips
GROUP BY payment_type
ORDER BY total_trips DESC;


-- =====================================
-- 4. Ticket médio
-- Pergunta: Qual o valor médio por corrida?
-- =====================================
SELECT 
    AVG(total_amount) AS avg_ticket
FROM fact_trips;


-- =====================================
-- 5. Corridas por dia
-- Pergunta: Volume ao longo do tempo
-- =====================================
SELECT 
    DATE(pickup_datetime) AS dia,
    COUNT(*) AS total_corridas
FROM fact_trips
GROUP BY dia
ORDER BY dia;