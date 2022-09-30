Shader "Unlit/AnimateGhost"
{
    Properties
    {
        _MainTex("RGBA", 2D) = "gray" {}
        _Opacity("Opacity", Range(0, 1)) = 0.5
        _ScaleParams ("Scale Params", vector) = (0.2, 1.0, 4.5, 0.0)
        _SwingXParams ("X Params", vector) = (1.0, 3.0, 1.0, 0.0)
        _SwingYParams ("Y Params", vector) = (1.0, 3.0, 0.3, 0.0)
        _SwingZParams ("Z Params", vector) = (1.0, 3.0, 1.0, 0.0)
        _ShakeYParams("Y Params", vector) = (20.0, 3.0, 0.3, 0.0)
    }
        SubShader
        {
           Tags { 
            "Queue" = "Transparent"
            "RenderType" = "Transparent"
            "ForceNoShadowCasting" = "True"
            "IgnoreProjector" = "True"
            }

            Pass
            {
                Name "FORWARD"
                Tags {
                    "LightMode" = "ForwardBase"
                }
                Blend One OneMinusSrcAlpha

                CGPROGRAM
                #pragma vertex vert
                #pragma fragment frag
                #include "UnityCG.cginc"
                #pragma multi_compile_fwdbase_fullshadows
                #pragma target 3.0

                uniform sampler2D _MainTex; uniform float4 _MainTex_ST;
                uniform half _Opacity;
                uniform float4 _ScaleParams;
                uniform float4 _SwingXParams;
                uniform float4 _SwingYParams;
                uniform float4 _SwingZParams;
                uniform float4 _ShakeYParams;

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
                float4 color : COLOR;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
                float4 color : COLOR;
            };

            #define TWO_PI 6.283185

            void AnimateGhost(inout float3 vertex, inout float3 color) {
                //缩放天使圈
                float scale = _ScaleParams.x * color.g * sin(frac(_Time.z * _ScaleParams.y) * TWO_PI);
                vertex.xyz *= 1.0 + scale;
                vertex.y -= _ScaleParams.z * scale;
                //幽灵摆动
                float swingX = _SwingXParams.x * sin(frac(_Time.z * _SwingXParams.y + vertex.y * _SwingXParams.z) * TWO_PI);
                float swingZ = _SwingZParams.x * sin(frac(_Time.z * _SwingXParams.y + vertex.y * _SwingXParams.z) * TWO_PI);
                vertex.xz += float2(swingX, swingZ) * color.r;
                //幽灵摇头
                float radY = radians(_ShakeYParams.x) * (1.0 - color.r) * sin(frac(_Time.z * _ShakeYParams.y - color.g * _ShakeYParams.z) * TWO_PI);
                float sinY, cosY = 0;
                sincos (radY, sinY, cosY);
                vertex.xz = float2(
                    vertex.x * cosY - vertex.z * sinY,
                    vertex.x* sinY + vertex.z * cosY
                    );
                //幽灵起伏
                float swingY = _SwingYParams.x * sin(frac(_Time.z * _SwingYParams.y - color.g * _SwingYParams.z) * TWO_PI);
                vertex.y += swingY;
                //处理顶点色
                float lightness = 1.0 + color.g * 1.0 + scale * 2.0;
                color = float3(lightness, lightness, lightness);
            }
            v2f vert (appdata v)
            {
                v2f o = (v2f)0;
                AnimateGhost(v.vertex.xyz, v.color.rgb);
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                o.color = v.color;
                return o;
            }

            half4 frag(v2f i) : COLOR
            {
                half4 var_MainTex = tex2D(_MainTex, i.uv);
                half3 finalRGB = var_MainTex.rgb * i.color.rgb;
                half opacity = var_MainTex.a * _Opacity;

                return half4(finalRGB * opacity, opacity);
            }
            ENDCG
        }
    }
}
