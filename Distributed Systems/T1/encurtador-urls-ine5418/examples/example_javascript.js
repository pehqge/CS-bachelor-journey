/**
 * Exemplo Node.js. Mesmo interceptador atende clientes em qualquer linguagem.
 */
'use strict';

const path = require('path');
const { URLShortenerClient } = require(
  path.join(__dirname, '..', 'clients', 'javascript', 'url_client.js')
);

const step = (t) => console.log(`\n-- ${t}`);

(async () => {
  const host = process.env.INTERCEPTOR_HOST || '127.0.0.1';
  const port = parseInt(process.env.INTERCEPTOR_PORT || '6000', 10);
  const cli = new URLShortenerClient(host, port);
  await cli.connect();
  try {
    step('ping');
    const pong = await cli.ping();
    console.log(`  ping -> ${pong}`);

    step('encurta duas URLs');
    const urls = [
      'https://nodejs.org/api/net.html',
      'https://learn.microsoft.com/azure/architecture/patterns/cache-aside',
    ];
    const codigos = [];
    for (const u of urls) {
      const r = await cli.encurta(u);
      console.log(`  encurta(${u}) -> rc=${r.rc} codigo=${r.codigo} curta=${r.urlCurta}`);
      if (r.rc !== 0) throw new Error('encurta falhou: ' + JSON.stringify(r));
      codigos.push(r.codigo);
    }

    step('resolve 3x — observe o source');
    for (let i = 0; i < 3; i++) {
      const r = await cli.resolve(codigos[0]);
      console.log(`  resolve(${codigos[0]}) #${i+1} -> rc=${r.rc} source=${r.source} url=${r.urlOriginal}`);
    }

    step('remove + tenta resolver de novo');
    const rcRemove = await cli.removeUrl(codigos[0]);
    console.log(`  removeUrl(${codigos[0]}) -> rc=${rcRemove}`);
    const after = await cli.resolve(codigos[0]);
    console.log(`  resolve(${codigos[0]}) após remoção -> rc=${after.rc} (esperado 404)`);

    step('listagem atual');
    const lst = await cli.listUrls();
    for (const it of lst.urls) {
      console.log('  -', JSON.stringify(it));
    }

    step('stats');
    const s = await cli.stats();
    console.log('  cache:  ', s.cache, `size=${s.cache_size}/${s.cache_max} ttl=${s.cache_ttl}s`);
    console.log('  circuit:', s.circuit);
  } finally {
    cli.close();
  }
})().catch((e) => {
  console.error('FALHA:', e);
  process.exitCode = 1;
});
