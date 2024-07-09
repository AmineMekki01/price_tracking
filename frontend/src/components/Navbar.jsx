import styled from 'styled-components';

const StyledNavbar = styled.nav`
    background-color: #f8f9fa; 
    padding: 0.5rem 1rem;
`;

const Container = styled.div`
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
`;

const NavbarBrand = styled.a`

    padding: 0.3125rem 1rem;
    font-size: 1.25rem;
    white-space: nowrap;
    // remove underline from link
    text-decoration: none;
`;

const NavbarToggle = styled.button`
    padding: 0.25rem 0.75rem;
    font-size: 1.25rem;
    background: none;
    border: none;
    &:focus {
        outline: none;
    }
`;

const NavbarCollapse = styled.div`
    display: flex;
    flex-basis: auto;
    flex-grow: 1;
    align-items: center;
`;

const Nav = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-left: auto;
`;

const NavLink = styled.a`
    padding: 0.5rem 1rem;
    text-decoration: none;
    color: #000;
    &:hover {
        text-decoration: underline;
    }
`;

const NavDropdown = styled.div`
  position: relative;
  display: inline-block;
`;

const NavDropdownToggle = styled.button`
  background: none;
  border: none;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  color: #000;
  &:hover {
    text-decoration: underline;
  }
`;

const NavDropdownMenu = styled.div`
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
  ${NavDropdown}:hover & {
    display: block;
  }
`;

const NavDropdownItem = styled.a`
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  &:hover {
    background-color: #ddd;
  }
`;

const NavDropdownDivider = styled.div`
  height: 1px;
  margin: 0.5rem 0;
  overflow: hidden;
  background-color: #e9ecef;
`;


function Navbar() {
  return (
    <StyledNavbar>
      <Container>
        <NavbarBrand href="#home">Price Tracker</NavbarBrand>
        <NavbarToggle aria-controls="basic-navbar-nav" />
        <NavbarCollapse id="basic-navbar-nav">
          <Nav>
            <NavLink href="/">Home</NavLink>
            <NavDropdown>
              <NavDropdownToggle>
                Search
              </NavDropdownToggle>
              <NavDropdownMenu>
                <NavDropdownItem href="/search-product">General Search</NavDropdownItem>
                <NavDropdownItem href="/direct-link-search">Direct Link or Exact Name Search</NavDropdownItem>
              </NavDropdownMenu>
            </NavDropdown>
            <NavLink href="/tracked-products">Tracked Products</NavLink>
          
          </Nav>
        </NavbarCollapse>
      </Container>
    </StyledNavbar>
  );
}

export default Navbar;
