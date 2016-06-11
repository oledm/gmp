import 'babel-polyfill'
import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux'
import { browserHistory, Router, Route, IndexRoute } from 'react-router'
import configureStore from './store/configureStore'
import App from './components/App'
import Login from './components/forms/Login'

const store = configureStore()

render(
    <Provider store={store}>
        <Router history={browserHistory}>
	    <Route path='/' component={App}>
                <Route path='/login' component={Login} />
                <Route path='/register' component={Login} />
	    </Route>
        </Router>
    </Provider>,
    document.getElementById('content')
)
