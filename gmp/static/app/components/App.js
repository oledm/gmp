import React from 'react'
import { connect } from 'react-redux'
import Toolbar from '../components/Toolbar'
import LoginForm from '../components/forms/LoginForm'

const App = ({ isAuthenticated }) => (
    <div>
        <Toolbar isAuthenticated={isAuthenticated} />
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

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
})

export default connect(mapStateToProps)(App)
