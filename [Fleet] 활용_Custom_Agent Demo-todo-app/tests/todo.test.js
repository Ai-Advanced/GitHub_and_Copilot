const { TodoApp } = require('../src/index');

function assert(condition, message) {
  if (!condition) throw new Error(`❌ FAIL: ${message}`);
  console.log(`✅ PASS: ${message}`);
}

// 기본 테스트
const app = new TodoApp();

// 추가 테스트
const todo = app.addTodo('테스트 할일');
assert(todo.id === 1, 'Todo 추가 시 ID가 1');
assert(todo.title === '테스트 할일', 'Todo 제목이 올바름');
assert(todo.completed === false, '새 Todo는 미완료 상태');

// 완료 테스트
app.completeTodo(1);
assert(app.getTodos()[0].completed === true, 'Todo 완료 처리');

// 삭제 테스트
app.deleteTodo(1);
assert(app.getTodos().length === 0, 'Todo 삭제 후 빈 배열');

console.log('\n🎉 모든 테스트 통과!');
