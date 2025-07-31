import styles from "./Task.module.scss"
export const Task = ({children}: {children: React.ReactNode}) => {
    return (
        <div className={styles.task}>
            {children}
        </div>
    )
}