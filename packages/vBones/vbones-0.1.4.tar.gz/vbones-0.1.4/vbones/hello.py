def say_hello(name=None):
    """
    간단한 인사말을 출력하는 함수
    
    Args:
        name (str, optional): 인사할 이름. 기본값은 None입니다.
    
    Returns:
        str: 인사말 메시지
    """
    if name:
        message = f"안녕하세요, {name}님! vBones에 오신 것을 환영합니다!"
    else:
        message = "안녕하세요! vBones에 오신 것을 환영합니다!"
    
    print(message)
    return message 