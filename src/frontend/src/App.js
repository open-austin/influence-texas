import React from 'react'
import { MuiThemeProvider } from '@material-ui/core/styles'
import { BrowserRouter as Router } from 'react-router-dom'
import ApolloClient from 'apollo-client'
import { ApolloProvider, useSubscription, useQuery } from '@apollo/react-hooks'
import { legTheme } from './theme'
import ScrollToTop from './ScrollToTop'
import Routes from './Routes'
import { split } from 'apollo-link'
import { HttpLink } from 'apollo-link-http'
import { WebSocketLink } from 'apollo-link-ws'
import { getMainDefinition } from 'apollo-utilities'
import { gql } from 'apollo-boost'
import { InMemoryCache } from 'apollo-cache-inmemory'
// Create an http link:
const httpLink = new HttpLink({
  uri: 'http://localhost:3003/graphql',
})

// Create a WebSocket link:
const wsLink = new WebSocketLink({
  uri: `ws://localhost:3003/subscriptions`,
  options: {
    reconnect: true,
  },
})

// using the ability to split links, you can send data to each link
// depending on what kind of operation is being sent
const link = split(
  // split based on operation type
  ({ query }) => {
    const definition = getMainDefinition(query)
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    )
  },
  wsLink,
  httpLink,
)

const client = new ApolloClient({
  link,
  cache: new InMemoryCache(),
  uri: 'http://localhost:3003/graphql',
})

const BOOK_SUBSCRIPTION = gql`
  subscription bookAdded($title: String!) {
    bookAdded(title: $title) {
      title
      author
    }
  }
`
const BOOKS_QUERY = gql`
  query {
    books {
      title
      author
    }
  }
`

function BookList() {
  const { data, loading } = useSubscription(BOOK_SUBSCRIPTION, {
    variables: { title: 'boo' },
  })
  const q = useQuery(BOOKS_QUERY)

  return (
    <div>
      {q.data && q.data.books.map((book) => <div>{book.title}</div>)}
      {data && <h4>Just added: {data.bookAdded.title}</h4>}
    </div>
  )
}

function App() {
  return (
    <ApolloProvider client={client}>
      <BookList />
    </ApolloProvider>
  )
}

export default App
