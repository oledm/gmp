import 'systemjs-hot-reloader/default-listener.js'
import 'babel-polyfill'
import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import RouterRenderer from './RouterRenderer'
import configureStore from './store/configureStore'

const store = configureStore()

let container = document.getElementById('content')

render(
    <Provider store={store}>
        <RouterRenderer />
    </Provider>,
    container
)
