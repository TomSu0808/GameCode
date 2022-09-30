Shader "Unlit/squence2"
{
    Properties
    {
        _MainTex("RGBA", 2D) = "gray" {}
        _Opacity("Opacity", Range(0, 1)) = 0.5
        _Sequence ("Squence", 2d) = "gray"{}
        _RowCount ("Row", int) = 1
        _ColCount ("ColCount", int) = 1
         _Speed ("Speed", Range(0.0, 15.0 ) ) = 1
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
                Name "FORWARD_AB"
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

                uniform sampler2D _MainTex; 
                uniform half _Opacity;

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


            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv0 = v.uv0;
               
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

        pass {
                 Name "FORWARD"
                Tags {
                    "LightMode" = "ForwardBase_AD"
                }
                Blend One One

                CGPROGRAM
                #pragma vertex vert
                #pragma fragment frag
                #include "UnityCG.cginc"
                #pragma multi_compile_fwdbase_fullshadows
                #pragma target 3.0

                uniform sampler2D _Sequence; uniform float4 _Squence_ST;
                 uniform half _Opacity;
                uniform half _RowCount;
                uniform half _ColCount;
                uniform half _Speed;
                uniform sampler2D _MainTex;


            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv0 : TEXCOORD0;
                float3 normal : NORMAL;
            };

            struct v2f
            {
                float2 uv0 : TEXCOORD0;
                float4 pos : SV_POSITION;
            };


            v2f vert(appdata v)
            {
                v2f o = (v2f)0;
                v.vertex.xyz += v.normal * 0.01;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv0 = TRANSFORM_TEX(v.uv0, _Squence);
                float id = floor(_Time.z * _Speed);
                float idV = floor(id / _ColCount);
                float idU = id - idV * _ColCount;
                float stepU = 1.0 / _ColCount;
                float stepV = 1.0 / _RowCount;
                float2 initUV = o.uv0 * float2(stepU, stepV) + float2(0.0, stepV * (_ColCount - 1.0));
                o.uv0 = initUV + float2 (idU * stepU, idV * stepV);

                return o;
            }

            half4 frag(v2f i) : COLOR
            {
                half4 var_Sequence = tex2D(_Sequence, i.uv0);
                half3 finalRGB = var_Sequence.rgb;
                half opacity = var_Sequence. a * _Opacity;
                return half4(finalRGB * opacity, opacity);
            }
            ENDCG
        }
    }
}
