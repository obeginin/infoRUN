export interface IUser {
    ID: number;
    Login: string;
    First_Name: string;
    Last_Name: string;
    Middle_Name: string;
    Email: string;
    BirthDate: Date | string;
    Sex: string;
    RoleName: string;
    Comment: string;
    IsActive: boolean;
    IsDeleted: boolean;
    RoleID: number;
    Password: string;
    Phone: string;
}