Shader "Unlit/LambertShader"
{
    Properties
    {
        _MainTex("Texture", 2D) = "white" {}
       _NormalTex("Texture", 2D) = ""{}
       _Diffuse("Diffuse", Color) = (1, 1, 1, 1)
    }
    SubShader
    {
        Tags { "LightingMode" = "ForwardBase" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag


            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float3 normal : NORMAL;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
                float3 worldNormal : NORMAL;
                float3 worldPos : TEXCOORD1;
            };

            sampler2D _MainTex;
            sampler2D _NormalTex;
            float4 _Diffuse;
            float4 _MainTex_ST;

            v2f vert (appdata v)
            {
                v2f o;
                o.uv = v.uv;

                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                // sample the texture
                //fixed4 col = tex2D(_MainTex, i.uv);
                float4 MainTex = tex2D(_MainTex, TRANSFORM_TEX(i.uv, _MainTex));


                float3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz  ;

                float3 worldLight = normalize(_WorldSpaceLightPos0.xyz);

                float3 worldNormal = normalize(i.worldNormal);

                float NdotL = max(0.0, dot(worldNormal, worldLight));

                float3 diffuse = _LightColor0.rgb * _Diffuse.rgb * NdotL;

                //fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb + max(0, dot(worldNormal, worldLight));

                fixed3 color = ambient + diffuse;

                return float4(color, 0);
            }
            ENDCG
        }
    }
           fallback"Diffuse"
}
