import { combineReducers } from 'redux'
import { reducer as formReducer } from 'redux-form'
import departments from './departments'
import auth from './auth'
import ui from './ui'

const rootReducer = combineReducers({
    departments,
    auth,
    ui,
    form: formReducer,
})

export default rootReducer
