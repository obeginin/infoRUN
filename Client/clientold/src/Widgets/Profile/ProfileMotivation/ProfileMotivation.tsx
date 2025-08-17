import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import { Paragraph } from "../../../ui/p/Paragraph";
import styles from "./ProfileMotivation.module.scss";
import blackboard from "../../../assets/blackboard.svg"
import { Button } from "../../../ui/buttonDeafault/Button";
export const ProfileMotivation = () => {
    return (
        <>
            <ProfileContentContainer color="purple">
                <div className={styles.motivation__exam}>
                    <Button style={{
                        backgroundColor: "var(--purple)",
                        border: "1px solid var(--bg)",
                        color: "var(--bg)"
                    }}>Цитата дня</Button>
                    <img src={blackboard} alt="" className={styles.motivation__exam__img}/>
                    <Paragraph color="white">Это всегда выглядит невозможным, пока не сделаешь.</Paragraph>
                </div>
            </ProfileContentContainer>
        </>
    );
};