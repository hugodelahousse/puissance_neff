import React from "react";
import { AppBar, Toolbar } from "@material-ui/core";
import Button from "@material-ui/core/Button";
import GamepadIcon from "@material-ui/icons/Gamepad";

const NavigationBar: React.FC = () => {
    return (
        <div className="Navigationbar">
            <AppBar position="static">
                <Toolbar>
                    <GamepadIcon/>
                    <Button color="inherit">Play</Button>
                    <Button color="inherit">Leaderboards</Button>
                </Toolbar>
            </AppBar>
        </div>
    )
};

export default NavigationBar;