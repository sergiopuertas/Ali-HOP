// api/alimentos.js
// Función serverless para Vercel
// Recuerda configurar en Vercel la variable de entorno NEON_DATABASE_URL

const { Client } = require('pg');

module.exports = async (req, res) => {
  // Leer query params si quieres filtrar por iones
  // const { ions } = req.query;

  const client = new Client({
    connectionString: process.env.NEON_DATABASE_URL,
    ssl: { rejectUnauthorized: false }
  });

  try {
    await client.connect();

    const result = await client.query(`
      SELECT alimento, image, sodio, potasio, fosforo
      FROM public.alimentos
      WHERE sodio IS NOT NULL OR potasio IS NOT NULL OR fosforo IS NOT NULL
    `);

    // Estructura inicial
    const foodData = {
      sodio: { recomendado: [], limitar: [], eliminar: [] },
      potasio: { recomendado: [], limitar: [], eliminar: [] },
      fosforo: { recomendado: [], limitar: [], eliminar: [] }
    };

    // Mapear valores categóricos directamente (campo en DB ya contiene "aconsejada", etc.)
    const catMap = {
      aconsejada: 'recomendado',
      limitada:   'limitar',
      desaconsejada: 'eliminar'
    };

    result.rows.forEach(r => {
      const item = { name: r.alimento, image: r.image };

      if (r.sodio != null) {
        const target = catMap[r.sodio] || 'recomendado';
        foodData.sodio[target].push({ ...item, category: r.sodio });
      }
      if (r.potasio != null) {
        const target = catMap[r.potasio] || 'recomendado';
        foodData.potasio[target].push({ ...item, category: r.potasio });
      }
      if (r.fosforo != null) {
        const target = catMap[r.fosforo] || 'recomendado';
        foodData.fosforo[target].push({ ...item, category: r.fosforo });
      }
    });

    res.status(200).json(foodData);
  } catch (error) {
    console.error('Error en la función /api/alimentos:', error);
    res.status(500).json({ error: 'Error al consultar la base de datos' });
  } finally {
    await client.end();
  }
};
