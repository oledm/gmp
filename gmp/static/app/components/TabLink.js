import React from 'react'
import { Link } from 'react-router'

class TabLink extends React.Component {
    render() {
        const isActive = this.context.router.isActive(this.props.to, true)
        const activeClass = isActive ? 'active' : null

        return (
            <li className={activeClass} role="presentation">
                <Link {...this.props}>{this.props.children}</Link>
            </li>
        )
    } 
}

TabLink.contextTypes = {
    router: React.PropTypes.object.isRequired
}

export default TabLink
