export interface User {
    ID: number;
    Login: string;
    Email: string;
    First_Name: string;
    Last_name: string;
    RoleName: string;
  }
  
export interface ErrorDetail {
    error: string;
    message: string;
  }