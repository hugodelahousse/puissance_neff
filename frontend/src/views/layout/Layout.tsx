import React, { ReactNode } from 'react';
import NavigationBar from '../navigationbar/NavigationBar';

interface ILayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: ILayoutProps) {
  return (
    <>
      <NavigationBar />
      {children}
    </>
  );
}
