def get_weather_icon_and_bg(weather_description):

    
    mapping = {
        "clear": ("☀️", "#87CEEB"),
        "rainy": ("🌧️", "#5F9EA0"),  
        "snowy": ("❄️", "#ADD8E6"),   
        "cloudy": ("☁️", "#D3D3D3"),  
        "stormy": ("🌩️", "#B0C4DE"),  
        "foggy": ("🌫️", "#A9A9A9"),   
    }

  
    default = ("🌈", "#FFD700")


    return mapping.get(weather_description.lower(), default)
