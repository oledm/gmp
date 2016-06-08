import memoize from 'lru-memoize';
import {createValidator, required, email} from '../../utils/validator';

const rules = createValidator({
    email: [required, email],
    password: [required],
});

export default memoize(10)(rules)
