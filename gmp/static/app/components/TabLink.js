import React from 'react'
import { Link, withRouter } from 'react-router'

class TabLink extends React.Component {
    render() {
        const isActive = this.props.router.isActive(this.props.to, true)
        const activeClass = isActive ? 'active' : null

        return (
            <li className={activeClass} role="presentation">
                <Link {...this.props}>{this.props.children}</Link>
            </li>
        )
    } 
}

export default withRouter(TabLink)
