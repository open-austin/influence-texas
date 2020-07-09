import { createMuiTheme } from '@material-ui/core/styles'

export const legTheme = createMuiTheme({
  typography: {
    button: {
      textTransform: 'none',
    },
  },
  palette: {
    primary: { dark: '#337168', main: '#3b9185', light: '#dbf1ed' },
  },
})

export const billTheme = createMuiTheme({
  palette: {
    primary: { dark: '#993333', main: '#cc6665', light: '#e7b3b3' },
  },
})

export const donorTheme = createMuiTheme({
  palette: {
    primary: { dark: '#2d3f77', main: '#344d99', light: '#d9dff3' },
  },
})
