// api/index.js
const { Client } = require('pg');

module.exports = async (req, res) => {
  // 1) Leer los iones pasados en la URL
  const { ions } = req.query;
  if (!ions) {
    return res
      .status(400)
      .json({ error: 'Pasa ?ions=sodio,potasio por ejemplo' });
  }
  const selected = ions
    .split(',')
    .map(i => i.trim().toLowerCase())
    .filter(i => ['sodio','potasio','fosforo'].includes(i));

  if (selected.length === 0) {
    return res
      .status(400)
      .json({ error: 'Al menos un ion válido: sodio, potasio o fosforo' });
  }

  // 2) Conexión a Neon
  const client = new Client({
    connectionString: process.env.NEON_URL_DATABASE,
    ssl: { rejectUnauthorized: false }
  });

  try {
    await client.connect();

    // 3) Traer todos los registros con valores en cualquiera de los 3 iones
    const { rows } = await client.query(`
      SELECT alimento, image, sodio, potasio, fosforo
      FROM public.alimentos
      WHERE sodio IS NOT NULL
         OR potasio IS NOT NULL
         OR fosforo IS NOT NULL
    `);

    // 4) Inicializar la estructura de salida solo para los iones seleccionados
    const foodData = {};
    selected.forEach(ion => {
      foodData[ion] = { recomendado: [], limitar: [], eliminar: [] };
    });

    // 5) Mapear categorías literales → listas
    const catMap = {
      aconsejada: 'recomendado',
      limitada:   'limitar',
      desaconsejada: 'eliminar'
    };

    // 6) Recorrer las filas y rellenar solo los iones que pedimos
    rows.forEach(r => {
      const item = { name: r.alimento, image: r.image };

      selected.forEach(ion => {
        const val = r[ion];
        if (val != null) {
          const target = catMap[val] || 'recomendado';
          foodData[ion][target].push(item);
        }
      });
    });

    // 7) Devolver JSON
    res.status(200).json(foodData);
  } catch (err) {
    console.error('Error en /api:', err);
    res.status(500).json({ error: 'Error interno al consultar BD' });
  } finally {
    await client.end();
  }
};
