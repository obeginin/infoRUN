import { ProfileContentContainer } from "../../Features/ProfileContentContainer/ProfileContentContainer";
import { Paragraph } from "../../ui/p/Paragraph";
import styles from "./ProfileMotivation.module.scss";
import blackboard from "../../assets/blackboard.svg"
export const ProfileMotivation = () => {
    return (
        <>
            <ProfileContentContainer>
                <div className={styles.motivation__exam}>
                    <img src={blackboard} alt="" className={styles.motivation__exam__img}/>
                    <Paragraph>Это всегда выглядит невозможным, пока не сделаешь.</Paragraph>
                </div>
            </ProfileContentContainer>
        </>
    );
};