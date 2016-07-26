import React from 'react'
import { browserHistory, Router, Route, IndexRoute } from 'react-router'
import App from './components/App'
import AuthForm from './components/forms/AuthForm'
import LoginForm from './components/forms/LoginForm'
import RegisterForm from './components/forms/RegisterForm'
import ProfileEditForm from './components/forms/ProfileEditForm'
import Dashboard from './components/Dashboard'
import requireAuthentication from './containers/AuthenticatedComponent'

const routes = {
    path: '/',
    component: App,
    indexRoute: {
        component: requireAuthentication(Dashboard)
    },
    childRoutes: [
        { path: '/login', component: AuthForm(LoginForm) },
        { path: '/register', component: AuthForm(RegisterForm) },
        { path: '/profile', component: ProfileEditForm },
    ]
};

export default class RouterRenderer extends React.Component {
    componentWillMount() {
        // https://github.com/capaj/systemjs-hot-reloader/issues/51
        // to work with jspm-live-reload
        // a little hack to help us rerender when this module is reloaded
        this.forceUpdate()
    }

    render() {
        return (
            <Router history={browserHistory} routes={routes} />
        )
    }
}
