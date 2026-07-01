/**
 * Cliente Node.js do interceptador. Mesmo protocolo da versão Python
 * (JSON + '\n' sobre TCP). API: encurta / resolve / removeUrl.
 */
'use strict';

const net = require('net');

class URLShortenerClient {
  constructor(host = '127.0.0.1', port = 6000, timeoutMs = 10000) {
    this.host = host;
    this.port = port;
    this.timeoutMs = timeoutMs;
    this._sock = null;
    this._buf = '';
    this._pending = []; // resolvers em ordem de chegada
    this._closedError = null;
  }

  connect() {
    if (this._sock) return Promise.resolve();
    return new Promise((resolve, reject) => {
      const sock = net.createConnection({ host: this.host, port: this.port });
      sock.setEncoding('utf8');
      const onError = (err) => {
        sock.removeAllListeners();
        reject(err);
      };
      sock.once('error', onError);
      sock.once('connect', () => {
        sock.removeListener('error', onError);
        sock.on('data', (chunk) => this._onData(chunk));
        sock.on('error', (err) => this._onClose(err));
        sock.on('close', () => this._onClose(new Error('conexão fechada')));
        this._sock = sock;
        resolve();
      });
    });
  }

  _onData(chunk) {
    this._buf += chunk;
    let nl;
    while ((nl = this._buf.indexOf('\n')) !== -1) {
      const line = this._buf.slice(0, nl);
      this._buf = this._buf.slice(nl + 1);
      const waiter = this._pending.shift();
      if (!waiter) continue;
      try {
        waiter.resolve(JSON.parse(line));
      } catch (e) {
        waiter.reject(e);
      }
    }
  }

  _onClose(err) {
    this._closedError = err;
    while (this._pending.length) {
      const w = this._pending.shift();
      w.reject(err);
    }
    this._sock = null;
  }

  close() {
    if (this._sock) {
      try { this._sock.end(); } catch (e) { /* noop */ }
      this._sock = null;
    }
  }

  _request(msg) {
    return this.connect().then(() => new Promise((resolve, reject) => {
      if (this._closedError) return reject(this._closedError);

      const ref = Symbol('req');
      const timer = setTimeout(() => {
        const idx = this._pending.findIndex((p) => p._ref === ref);
        if (idx >= 0) this._pending.splice(idx, 1);
        reject(new Error(`timeout após ${this.timeoutMs}ms`));
      }, this.timeoutMs);

      const waiter = {
        _ref: ref,
        resolve: (v) => { clearTimeout(timer); resolve(v); },
        reject: (e) => { clearTimeout(timer); reject(e); },
      };
      this._pending.push(waiter);
      try {
        this._sock.write(JSON.stringify(msg) + '\n');
      } catch (e) {
        const idx = this._pending.indexOf(waiter);
        if (idx >= 0) this._pending.splice(idx, 1);
        clearTimeout(timer);
        reject(e);
      }
    }));
  }

  async encurta(urlOriginal) {
    let resp;
    try {
      resp = await this._request({ action: 'encurta', url: urlOriginal });
    } catch (e) {
      return { rc: -1, codigo: null, urlCurta: null, error: String(e) };
    }
    if (resp.status === 'ok') {
      return { rc: 0, codigo: resp.codigo, urlCurta: resp.url_curta };
    }
    return { rc: resp.code ?? -2, codigo: null, urlCurta: null, error: resp.message };
  }

  async resolve(codigoCurto) {
    let resp;
    try {
      resp = await this._request({ action: 'resolve', codigo: codigoCurto });
    } catch (e) {
      return { rc: -1, urlOriginal: null, error: String(e) };
    }
    if (resp.status === 'ok') {
      return { rc: 0, urlOriginal: resp.url_original, source: resp.source };
    }
    return { rc: resp.code ?? -2, urlOriginal: null, error: resp.message };
  }

  async removeUrl(codigoCurto) {
    let resp;
    try {
      resp = await this._request({ action: 'remove', codigo: codigoCurto });
    } catch (e) {
      return -1;
    }
    return resp.status === 'ok' ? 0 : (resp.code ?? -2);
  }

  async listUrls() {
    let resp;
    try {
      resp = await this._request({ action: 'list' });
    } catch (e) {
      return { rc: -1, urls: [], error: String(e) };
    }
    if (resp.status === 'ok') return { rc: 0, urls: resp.urls };
    return { rc: resp.code ?? -2, urls: [], error: resp.message };
  }

  async stats() {
    try {
      return await this._request({ action: 'stats' });
    } catch (e) {
      return { status: 'error', message: String(e) };
    }
  }

  async ping() {
    try {
      const r = await this._request({ action: 'ping' });
      return r.status === 'ok';
    } catch (e) {
      return false;
    }
  }
}

async function encurta(urlOriginal, host = '127.0.0.1', port = 6000) {
  const c = new URLShortenerClient(host, port);
  try { return await c.encurta(urlOriginal); } finally { c.close(); }
}
async function resolve(codigoCurto, host = '127.0.0.1', port = 6000) {
  const c = new URLShortenerClient(host, port);
  try { return await c.resolve(codigoCurto); } finally { c.close(); }
}
async function removeUrl(codigoCurto, host = '127.0.0.1', port = 6000) {
  const c = new URLShortenerClient(host, port);
  try { return await c.removeUrl(codigoCurto); } finally { c.close(); }
}

module.exports = { URLShortenerClient, encurta, resolve, removeUrl };
