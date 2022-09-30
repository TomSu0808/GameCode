Shader "Unlit/Scaling"
{
    Properties
    {
        _MainTex("RGBA", 2D) = "gray" {}
        _Opacity("Opacity", Range(0, 1)) = 0.5
        _ScaleRange ("Move Range", Range(0.0, 3.0)) = 1.0
        _ScaleSpeed("Move Speed", Range(0.0, 3.0)) = 1.0
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
             uniform float _ScaleRange;
             uniform float _ScaleSpeed;


             struct appdata
            {
                float4 vertex : POSITION;
                float2 uv0 : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv0 : TEXCOORD0;
                float4 pos : SV_POSITION;
            };

            #define TWO_PI 6.283185

            void Scaling(inout float3 vertex) {
               vertex.y *= 1.0 + _ScaleRange * sin(frac(_Time.z * _ScaleSpeed) * TWO_PI);
            }

            v2f vert (appdata v)
            {
                v2f o = (v2f)0;
                Scaling(v.vertex.xyz);
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv0 = TRANSFORM_TEX(v.uv0, _MainTex);
                
                return o;
            }

            half4 frag(v2f i) : COLOR
            {
                half4 var_MainTex = tex2D(_MainTex, i.uv0);
                half3 finalRGB = var_MainTex.rgb;
                half opacity = var_MainTex.a * _Opacity;

                return half4(finalRGB * opacity, opacity);
            }
            ENDCG
        }
    }
}
