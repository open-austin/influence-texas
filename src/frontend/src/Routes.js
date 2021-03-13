import React from 'react'
import { Tabs, Tab, makeStyles } from '@material-ui/core'
import { Route, useHistory, Switch } from 'react-router-dom'
import LegislatorsPage from 'components/LegislatorsPage'
import Logo from 'components/Logo'
import FindReps from 'components/FindReps'
import About from 'components/About'
import BillsPage from 'components/BillsPage'
import DonorsPage from 'components/DonorsPage'
import PolicyAreasPage from 'components/PolicyAreasPage'
import LegislatorDetailPage from 'components/LegislatorDetailPage'
import DonorDetailPage from 'components/DonorDetailPage'
import BillDetailPage from 'components/BillDetailPage'
import PersonOutlineRounded from '@material-ui/icons/PersonOutlineRounded'
import ReceiptRounded from '@material-ui/icons/ReceiptRounded'
import MonetizationOnRounded from '@material-ui/icons/MonetizationOnRounded'
// import PublicRounded from "@material-ui/icons/PublicRounded";
import SearchAll, { SearchResults } from 'components/SearchAll'
import { TabWrapper } from 'components/SimpleTabs'
import CustomLink from 'components/CustomLink'
import { MuiThemeProvider } from '@material-ui/core/styles'
import { billTheme, legTheme, donorTheme } from 'theme'

const useStyles = makeStyles({
  billsTab: {
    '&.MuiTab-textColorPrimary.Mui-selected': {
      color: billTheme.palette.primary.main,
    },
  },
  donorTab: {
    '&.MuiTab-textColorPrimary.Mui-selected': {
      color: donorTheme.palette.primary.main,
    },
  },
  wrapper: {
    '& .MuiTabs-indicator': {
      backgroundColor: legTheme.palette.grey[600],
    },
  },
})

function Nav() {
  const classes = useStyles()
  const history = useHistory()
  if (
    history.location.pathname.includes('searchAll') ||
    history.location.pathname.includes('findReps') ||
    history.location.pathname.includes('about')
  ) {
    return null
  }
  return (
    <TabWrapper>
      <nav style={{ margin: '1em 0' }} className={classes.wrapper}>
        <Tabs
          variant="fullWidth"
          indicatorColor="primary"
          textColor="primary"
          value={history.location.pathname.split('/')[1] || 'legislators'}
        >
          <Tab
            label={
              <>
                <PersonOutlineRounded /> Legislators
              </>
            }
            color={legTheme.palette.primary}
            value="legislators"
            onClick={() => history.push('/legislators')}
          />
          <Tab
            label={
              <>
                <ReceiptRounded /> Bills
              </>
            }
            value="bills"
            className={classes.billsTab}
            onClick={() => history.push('/bills')}
          />
          <Tab
            label={
              <>
                <MonetizationOnRounded /> Donors
              </>
            }
            value="donors"
            className={classes.donorTab}
            onClick={() => history.push('/donors')}
          />
        </Tabs>
      </nav>
    </TabWrapper>
  )
}

function ThemedBody({ children }) {
  const { location } = useHistory()
  let theme = legTheme
  if (location.pathname.includes('/bills')) {
    theme = billTheme
  }
  if (location.pathname.includes('/donors')) {
    theme = donorTheme
  }
  return <MuiThemeProvider theme={theme}>{children}</MuiThemeProvider>
}

export default function Routes() {
  return (
    <div>
      <Logo />
      <div style={{ float: 'right', margin: '1.25rem 0 0 1rem' }}>
        <CustomLink to="/about">About</CustomLink>
      </div>
      <div style={{ float: 'right', margin: '1.25rem 0 0 1rem' }}>
        <CustomLink to="/findReps">Find Your Reps</CustomLink>
      </div>
      <div style={{ float: 'right', margin: '1.25rem 0 0 1rem' }}>
        <CustomLink to="/">Home</CustomLink>
      </div>
      <SearchAll />
      <Nav />

      <ThemedBody>
        <Switch>
          <Route path="/searchAll/:searchQuery">
            <SearchResults />
          </Route>
          <Route path="/findReps">
            <FindReps />
          </Route>
          <Route path="/about">
            <About />
          </Route>
          <Route path="/bills/bill/:id">
            <BillDetailPage />
          </Route>
          <Route path="/bills">
            <BillsPage />
          </Route>
          <Route path="/donors/donor/:id">
            <DonorDetailPage />
          </Route>
          <Route path="/donors">
            <DonorsPage />
          </Route>
          <Route path="/policy-areas">
            <PolicyAreasPage />
          </Route>
          <Route path="/legislators/legislator/:id">
            <LegislatorDetailPage />
          </Route>
          <Route path="/legislators">
            <LegislatorsPage />
          </Route>
          <LegislatorsPage />
        </Switch>
      </ThemedBody>
    </div>
  )
}
