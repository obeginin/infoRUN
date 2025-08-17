import type { IUser } from "../../../../interface/user.interface";
import styles from "./TableUsers.module.scss";
import { Popup } from "../Popup/Popup";
import { useAdminStore } from "../../../../Pages/Admin/store";
export const TableUsers = () => {
  const { isVisiblePopup, setVisiblePopup, currentUser, filteredUsers } =
    useAdminStore();

  return (
    <>
      <table className={styles.table}>
        <thead>
          <tr>
            <th scope="col">id</th>
            <th scope="col">Логин</th>
            <th scope="col">Email</th>
            <th scope="col">Имя</th>
            <th scope="col">Фамилия</th>
            <th scope="col">Роль</th>
            <th scope="col">Статус</th>
            <th scope="col"></th>
          </tr>
        </thead>

        <tbody>
          {filteredUsers().length > 0 ? (
            filteredUsers().map((item: IUser) => (
              <tr key={item.ID}>
                <td>{item.ID}</td>
                <td>{item.Login}</td>
                <td>{item.Email.slice(0, 20)}</td>
                <td>{item.First_Name}</td>
                <td>{item.Last_Name}</td>
                <td>{item.RoleName}</td>
                <td>
                  {item.IsActive.toString() === "true" ? (
                    <span
                      className="pi pi-check"
                      style={{ color: "green" }}
                    ></span>
                  ) : (
                    <span
                      className="pi pi-times"
                      style={{ color: "red" }}
                    ></span>
                  )}
                </td>
                <td>
                  {item.RoleName !== "Админ" && (
                    <span
                      className="pi pi-ellipsis-v"
                      onClick={() => setVisiblePopup(item)}
                    ></span>
                  )}
                {isVisiblePopup && currentUser?.ID === item.ID && <Popup />}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={6}>Пользователи не найдены</td>
            </tr>
          )}
        </tbody>
      </table>
    </>
  );
};

export default TableUsers;
