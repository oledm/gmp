import React from 'react'

const Todo = ({ text, completed, onClick}) => {
    return (
        <li
            style={{
                textDecoration: completed ? 'line-through': 'none'
            }}
            onClick={onClick}
        >
            {text}
        </li>
    )
}

export default Todo
