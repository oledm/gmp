import { IS_SUBMITTING } from '../constants/index'

export default (state = {
    isSubmitting: false
}, action) => {
    switch (action.type) {
        case IS_SUBMITTING:
            return {...state,
                isSubmitting: action.isSubmitting
            }
        default:
            return state
    }
}
