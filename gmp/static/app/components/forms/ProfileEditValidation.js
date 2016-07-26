import memoize from 'lru-memoize';
import {createValidator, required, email} from '../../utils/validator';

const rules = createValidator({
    last_name: [required],
    first_name: [required],
    middle_name: [required],
    password: [required],
});

export default memoize(10)(rules)
