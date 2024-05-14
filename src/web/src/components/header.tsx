import { Avatar, Header, Octicon } from "@primer/react";
import { MortarBoardIcon } from "@primer/octicons-react";

const AppHeader = () => {
  return (
    <Header>
      <Header.Item>
        <Header.Link
          href="#"
          sx={{
            fontSize: 2,
          }}
        >
          <Octicon
            icon={MortarBoardIcon}
            size={32}
            sx={{
              mr: 2,
            }}
          />
          <span>Your AI Creative Team</span>
        </Header.Link>
      </Header.Item>
      <Header.Item full></Header.Item>
      <Header.Item>Sarah Lee</Header.Item>
      <Header.Item>
        <Avatar src="/people/sarahlee.jpg" size={40} />
      </Header.Item>
    </Header>
  );
};

export default AppHeader;
