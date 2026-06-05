/**
 * Demo Todo App - Feature Builder 에이전트 테스트용
 * 이 파일은 간단한 Todo CRUD 기능만 있습니다.
 * 에이전트에게 새 기능을 추가해달라고 요청해보세요!
 */

class TodoApp {
  constructor() {
    this.todos = [];
    this.nextId = 1;
  }

  addTodo(title) {
    const todo = {
      id: this.nextId++,
      title,
      completed: false,
      createdAt: new Date().toISOString()
    };
    this.todos.push(todo);
    return todo;
  }

  getTodos() {
    return this.todos;
  }

  completeTodo(id) {
    const todo = this.todos.find(t => t.id === id);
    if (!todo) throw new Error(`Todo ${id} not found`);
    todo.completed = true;
    return todo;
  }

  deleteTodo(id) {
    const index = this.todos.findIndex(t => t.id === id);
    if (index === -1) throw new Error(`Todo ${id} not found`);
    return this.todos.splice(index, 1)[0];
  }
}

module.exports = { TodoApp };
