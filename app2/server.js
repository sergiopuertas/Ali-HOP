// server.js
require('dotenv').config();

const express = require('express');
const { Client } = require('pg');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

// Sirve tu carpeta pública
app.use(express.static(path.join(__dirname, 'public')));

app.get('/api', async (req, res) => {
  const client = new Client({
  connectionString: process.env.NEON_URL_DATABASE,
  ssl: { rejectUnauthorized: false }
});

  await client.connect();
  const result = await client.query(`
    SELECT alimento, image, sodio, potasio, fosforo
    FROM alimentos
    WHERE sodio IS NOT NULL OR potasio IS NOT NULL OR fosforo IS NOT NULL
  `);
  await client.end();

  const foodData = {
    sodio: { recomendado: [], limitar: [], eliminar: [] },
    potasio: { recomendado: [], limitar: [], eliminar: [] },
    fosforo: { recomendado: [], limitar: [], eliminar: [] }
  };

  const categories = {
    recomendado: "aconsejada",
    limitar: "limitada",
    eliminar: "desaconsejada"
  };

  result.rows.forEach(r => {
    const item = {name: r.alimento, image: r.image};
    if (r.sodio != null) {
      if (r.sodio === 'aconsejada') foodData.sodio.recomendado.push({...item, category: categories.recomendado});
      else if (r.sodio  === 'limitada') foodData.sodio.limitar.push({...item, category: categories.limitada});
      else foodData.sodio.eliminar.push({...item, category: categories.desaconsejada});
    }
    if (r.potasio != null) {
      if (r.potasio  === 'aconsejada') foodData.potasio.recomendado.push({...item, category: categories.recomendado});
      else if (r.potasio === 'limitada') foodData.potasio.limitar.push({...item, category: categories.limitada});
      else foodData.potasio.eliminar.push({...item, category: categories.desaconsejada});
    }
    if (r.fosforo != null) {
      if (r.fosforo  === 'aconsejada') foodData.fosforo.recomendado.push({...item, category: categories.recomendado});
      else if (r.fosforo === 'limitada') foodData.fosforo.limitar.push({...item, category: categories.limitada});
      else foodData.fosforo.eliminar.push({...item, category: categories.desaconsejada});
    }
  });

  res.json(foodData);
});

app.listen(port, () => console.log(`Servidor escuchando en http://localhost:${port}`));
