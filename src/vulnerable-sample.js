// ⚠️ 이 파일은 GHAS 교육용 샘플입니다.
// 의도적으로 보안 취약점을 포함하고 있습니다.
// 절대 프로덕션에서 사용하지 마세요!

const express = require('express');
const mysql = require('mysql');

const app = express();
app.use(express.json());

const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'password123',  // CWE-798: 하드코딩된 자격증명
  database: 'myapp'
});

// CWE-89: SQL Injection 취약점
app.get('/users', (req, res) => {
  const name = req.query.name;
  const query = "SELECT * FROM users WHERE name = '" + name + "'";
  db.query(query, (err, results) => {
    if (err) {
      console.log(err);
      res.status(500).send('Error');
      return;
    }
    res.json(results);
  });
});

// CWE-79: Cross-Site Scripting (XSS) 취약점
app.get('/search', (req, res) => {
  const keyword = req.query.q;
  res.send(`<h1>검색 결과: ${keyword}</h1>`);
});

// CWE-22: Path Traversal 취약점
app.get('/file', (req, res) => {
  const filename = req.query.name;
  res.sendFile('/uploads/' + filename);
});

// CWE-78: OS Command Injection 취약점
const { exec } = require('child_process');
app.get('/ping', (req, res) => {
  const host = req.query.host;
  exec('ping -c 4 ' + host, (err, stdout) => {
    res.send(stdout);
  });
});

// CWE-327: 취약한 암호화 알고리즘 사용
const crypto = require('crypto');
app.get('/hash', (req, res) => {
  const data = req.query.data;
  const hash = crypto.createHash('md5').update(data).digest('hex');
  res.json({ hash });
});

// CWE-918: Server-Side Request Forgery (SSRF)
const http = require('http');
app.get('/fetch', (req, res) => {
  const url = req.query.url;
  http.get(url, (response) => {
    let data = '';
    response.on('data', chunk => data += chunk);
    response.on('end', () => res.send(data));
  });
});

// CWE-502: Insecure Deserialization
app.post('/deserialize', (req, res) => {
  const serialized = req.body.data;
  const obj = eval('(' + serialized + ')');
  res.json(obj);
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
