import React from "react";
import { Switch, Route, Link } from "react-router-dom";
import LoginModal from "./LoginModal";
import Signup from "./Signup";

function App() {
  return (
    <div className="App">
      <h1>Hello, World!</h1>
      <nav>
        <Link className={"nav-link"} to={"/"}>
          Home
        </Link>
        <Link className={"nav-link"} to={"/login/"}>
          Login
        </Link>
        <Link className={"nav-link"} to={"/signup/"}>
          Signup
        </Link>
      </nav>
      <Switch>
        <Route exact path={"/login/"} component={LoginModal} />
        <Route exact path={"/signup/"} component={Signup} />
        <Route
          path={"/"}
          reunder={() => {
            <div>Home again</div>;
          }}
        />
      </Switch>
    </div>
  );
}

export default App;
