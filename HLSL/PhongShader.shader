Shader "Unlit/PhongShader"
{
    Properties
    {
        _MainTex("Texture", 2D) = "white" {}
       _NormalMap("NormalMap", 2D) = ""{}
       _Diffuse("Diffuse", Color) = (1, 1, 1, 1)
        _Specular("Specular" , Color) = (1, 1, 1, 1)
        _Gloss("Gloss", Range(1, 255)) = 20
         _LocalNormalSild("LocalNormal", Range(0, 1)) = 0
    }
    SubShader
    {
        Tags { "LightingMode" = "ForwardBase" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            sampler2D _MainTex;
    uniform sampler2D _NormalMap; uniform float4 _NormalMap_ST;
            float4 _Diffuse;
            float4 _Specular;
            float _Gloss;
            float4 _MainTex_ST;
            float _LocalNormalSild;

             struct appdata
            {
                float4 vertex : POSITION;
                float3 normal : NORMAL;
                float4 tangent : TANGENT;
                float2 texcoord0 : TEXCOORD0;
               
            };

            struct v2f
            {
                float4 pos : SV_POSITION;
                float3 color : COLOR;                
                float3 worldNormal : NORMAL;
                float2 uv0 : TEXCOORD0;
                float3 normalDir : TEXCOOD1;
                float3 tangentDir : TEXCOORD2;
                float3 bitangentDir : TEXCOORD3;
                float3 worldPos : TEXCOORD4;

            };

            v2f vert(appdata v)
            {
                v2f o;
                o.uv0 = v.texcoord0;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;

                //caculate normal tangent
                o.normalDir = UnityObjectToWorldNormal(v.normal);
                o.tangentDir = normalize(mul(unity_ObjectToWorld, float4(v.tangent.xyz, 0.0)).xyz);
                o.bitangentDir = normalize(cross(o.normalDir, o.tangentDir) * v.tangent.w);

                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
               float4 MainTex = tex2D(_MainTex, TRANSFORM_TEX(i.uv0, _MainTex));

                //环境光
                float3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz * _Diffuse * MainTex.rgb;
                //归一化光方向
                float3 worldLight = normalize(_WorldSpaceLightPos0.xyz);
                // 世界空间的法线
                float3 worldNormal = normalize(i.worldNormal);

                //normal
                i.normalDir = worldNormal;
                float3x3 tangentTransform = float3x3(i.tangentDir, i.bitangentDir, i.normalDir);

                //normal map
                float3 normalLocal = UnpackNormal (tex2D(_NormalMap, TRANSFORM_TEX(i.uv0, _NormalMap)));

                float3 normalWorld = normalize(mul(normalLocal.rgb, tangentTransform));

                //lambert
                float3 finiNormal = lerp(worldNormal, normalWorld, _LocalNormalSild);

                float NdotL = max(0.0, dot(finiNormal, worldLight));

                float3 diffuse = _LightColor0.rgb * _Diffuse.rgb * NdotL;

                //fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb + max(0, dot(worldNormal, worldLight));

               // fixed3 color = ambient + diffuse;

              //Reflection Caculate
                fixed3 reflectDir = normalize(reflect(-worldLight, finiNormal));
                //caculate position in world space
                float3 viewDir = normalize(_WorldSpaceCameraPos.xyz - i.worldPos.xyz);

                //simple the VdotL
                float VdotR = max(0.0, dot(reflectDir, viewDir));
                //specular
                float3 specular = _LightColor0.rgb * _Specular.rgb * pow(VdotR , _Gloss);

                //phong funtion : diffuse + Ambient + Specular
                
                float3 color = diffuse + ambient + specular;

                return fixed4 (color.rgb, 1.0);
            }
            ENDCG
        }
    }
}
