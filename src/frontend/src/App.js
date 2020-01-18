import React from "react";
import { MuiThemeProvider } from "@material-ui/core/styles";
import { BrowserRouter as Router } from "react-router-dom";
import ApolloClient from "apollo-boost";
import { ApolloProvider } from "@apollo/react-hooks";
import { legTheme } from "./theme";
import ScrollToTop from "./ScrollToTop";
import Routes from "./Routes";

const client = new ApolloClient({
  uri:
    process.env.NODE_ENV === "development"
      ? "http://localhost:5120/graphql/"
      : "/graphql/"
});

function App() {
  return (
    <ApolloProvider client={client}>
      <Router>
        <MuiThemeProvider theme={legTheme}>
          <ScrollToTop>
            <Routes />
          </ScrollToTop>
        </MuiThemeProvider>
      </Router>
    </ApolloProvider>
  );
}

export default App;
