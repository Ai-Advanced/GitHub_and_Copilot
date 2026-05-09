// 의도적으로 레거시 스타일로 작성된 코드
// Modernizer 에이전트 테스트용 샘플
var express = require('express');
var router = express.Router();
var mysql = require('mysql');

var db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'password123',
  database: 'myapp'
});

router.get('/users', function(req, res) {
  var query = "SELECT * FROM users WHERE name = '" + req.query.name + "'";
  db.query(query, function(err, results) {
    if (err) {
      console.log(err);
      res.status(500).send('Error');
    }
    res.json(results);
  });
});

router.post('/users', function(req, res) {
  var name = req.body.name;
  var email = req.body.email;
  var age = req.body.age;

  if (name == '' || email == '') {
    res.status(400).send('Bad request');
    return;
  }

  var query = "INSERT INTO users (name, email, age) VALUES ('" + name + "', '" + email + "', " + age + ")";
  db.query(query, function(err, result) {
    if (err) {
      console.log('error: ' + err);
      res.status(500).send('Error');
    }
    res.json({id: result.insertId, name: name, email: email});
  });
});

router.delete('/users/:id', function(req, res) {
  db.query("DELETE FROM users WHERE id = " + req.params.id, function(err) {
    if (err) console.log(err);
    res.send('deleted');
  });
});

module.exports = router;
