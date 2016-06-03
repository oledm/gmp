import { REQUEST_DEPARTMENTS, RECEIVE_DEPARTMENTS } from '../constants/index'

const departments = (state = {
    isFetching: false,
    departments: {}
}, action) => {
    switch(action.type) {
        case REQUEST_DEPARTMENTS:
            return {...state,
                isFetching: true
            }
        case RECEIVE_DEPARTMENTS:
            return {...state,
                isFetching: false,
                departments: action.departments
            }
        default:
            return state
    }
}

export default departments
