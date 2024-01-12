type AuthLayoutProps = {
    children:React.ReactNode
}


export default function AuthLayout({children}:AuthLayoutProps){

    return (
        <div className={"flex flex-1 h-screen w-screen"}>
            <div className={"flex w-8/12"}></div>
            <div className={"flex w-4/12"}>
                {children}
            </div>
        </div>
    );

}
