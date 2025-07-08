interface ParagraphProps {
    children: React.ReactNode;
    size?: 'large' | 'medium' | 'base' | 'small' | 'tiny';
    f_weight?: 'light' | 'extra_bold';
}


export const Paragraph = ({ children, size='base', f_weight='light' }: ParagraphProps) => {
    return (
    <p style={{ 
        fontSize: `var(--${size})`,
        fontWeight: `var(--fw_${f_weight})`,
        fontFamily: '`Lato` sans-serif'
    }}>
        {children}
    </p>
    )
};