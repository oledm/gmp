import React from 'react';

const Messages = ({show, children}) => 
    show
        ? 
            <div className="help-block" role="alert">
                {children}
            </div>
        :
            null

export default Messages
