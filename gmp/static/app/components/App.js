import React from 'react'
import Toolbar from '../components/Toolbar'
import LoginForm from '../components/forms/LoginForm'

const App = () => (
    <div>
        <Toolbar />
        <LoginForm />
         <div className="tabbable">
            <ul className="nav nav-tabs">
                <li data-toggle="tab" ui-sref-active="active" className="active item" role="presentation">
                    <a ui-sref="login">
                        Вход
                    </a>
                </li>
                <li data-toggle="tab" ui-sref-active="active" className="active item" role="presentation">
                    <a ui-sref="register">
                        Регистрация
                    </a>
                </li>
            </ul>
        </div>
    </div>
)

export default App
