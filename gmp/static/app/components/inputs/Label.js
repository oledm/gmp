import React from 'react';

const Label = ({htmlFor, children}) =>
    <label className="control-label" htmlFor={htmlFor}>
        {children}
    </label>;

export default Label