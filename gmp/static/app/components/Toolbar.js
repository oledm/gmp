import React from 'react'

const Toolbar = ({ isAuthenticated }) => (
    !isAuthenticated
        ? null
        : <nav className="navbar navbar-default">
      <div className="container-fluid">
	    <div className="navbar-header">
	      <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
		<span className="sr-only">Toggle navigation</span>
		<span className="icon-bar"></span>
		<span className="icon-bar"></span>
		<span className="icon-bar"></span>
	      </button>
	      <a className="navbar-brand" href="/">
		  <strong>АКФОД</strong>
	      </a>
	    </div>
	<div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
	   <ul className="nav navbar-nav">
	       <li data-target="#bs-example-navbar-collapse-1">
		    <a href="#">
		    Link
		    </a>
	       </li>
	   </ul>

	  <ul className="nav navbar-nav navbar-right">

	  <div className="navbar-text hidden-sm hidden-xs">ФИО</div>
	    <li className="danger">
		<a href="#">
		 Выход
		</a>
	    </li>
	  </ul>
	</div>
      </div>
    </nav>
)

export default Toolbar
