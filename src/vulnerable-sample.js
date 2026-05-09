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

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
