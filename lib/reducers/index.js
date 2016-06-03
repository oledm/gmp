import { combineReducers } from 'redux'
import todos from './todos'
import visibilityFilter from './visibilityFilter'
import departments from './departments'
import {reducer as formReducer} from 'redux-form';

const rootReducer = combineReducers({
    todos,
    visibilityFilter,
    departments,
    form: formReducer,
})

export default rootReducer
