import React from 'react';

const InputLabel = ({htmlFor, children}) =>
    <label className="control-label" htmlFor={htmlFor}>
        {children}
    </label>;

export default InputLabel
