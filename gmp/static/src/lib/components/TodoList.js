import React from 'react'
import Todo from './Todo'

const TodoList = ({ todos, onTodoClick }) => {
    if (todos.length === 0) {
        return <div>Add todos</div>
    }

    return (
        <div>
            <ul>
                {todos.map(todo => 
                    <Todo
                        key={todo.id}
                        {...todo}
                        onClick={() => onTodoClick(todo.id)}
                    />
                )}
            </ul>
        </div>
    )
}

export default TodoList
