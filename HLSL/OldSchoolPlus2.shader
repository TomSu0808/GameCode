Shader "Unlit/OldSchoolPlus2"
{
    Properties
    {
        [Header(Texture)]
               [HideInInspect] _MainTex("BaseColTex", 2d) = "white"{}
                _NormTex("NormalTex", 2d) = "bump"{}
                _SpecTex("SpecTex", 2d) = "gray"{}
                _EmitTex("EmbientTex", 2d) = "black" {}
                _CubeMap("CubeMapTex", cube) = "_Skybox"{}
         [Header(Diffuse)]
                _MainCol ("BaseColor", color) = (0.5, 0.5, 0.5, 1)
                _EnvDiffInt("Envirment Diffuse Strength", Range(0, 1)) = 0.2
                _EnvUpCol("EnvUpColr", color) = (1, 1, 1, 1)
                _EnvSideCol("EnvSideCol",color) = (0.5, 0.5, 0.5, 1)
                _EnvDownColor("EnvDownCol" , color) = (0, 0, 0, 1)
          [Header(Specular)]
                 [PowerSlider(2)]_SpecPow ("SpecPow", Range(1, 90)) = 30
                _EnvSpecInt ("Envirment Minor Reflect Strength", Range(0,5)) = 0.2
                _FresnelPow ("FresnelPow", Range(0, 5) ) = 1
                _CubeMapMip("MapMip", Range(0,7)) = 0
          [Header(Emission)]
                _EmitInt("Emission Strength", Range(1, 10)) = 1
    }

        SubShader
                {
                    Tags { "RenderType" = "Opaque" }

                    Pass
                    {
                        Name "FORWARD"
                        Tags {
                            "LightingMode" = "ForwardBase"
                        }
                        CGPROGRAM
                        #pragma vertex vert
                        #pragma fragment frag
                        #include "UnityCG.cginc"
                        #pragma multi_compile_fwdbase_fullshadows
                        #pragma target 3.0
                        #include "AutoLight.cginc"
                        #include "Lighting.cginc"

                    //texture
                    uniform sampler2D _MainTex;
                    uniform sampler2D _NormTex;
                    uniform sampler2D _SpecTex;
                    uniform sampler2D _EmitTex;
                    uniform sampler2D _CubeMap;
                    //Diffuse
                    uniform float3 _MainCol;
                    uniform float _EnvDiffInt;
                    uniform float3  _EnvUpCol;
                    float3 _EnvSideCol;
                    float3 _EnvDownCol;
                    //Specular
                    uniform float _SpecPow;
                    uniform float _FresnelPow;
                    uniform float _EnvSpecInt;
                    uniform float _CubeMapMip;
                    //Emission
                    uniform float _EmitInt;

                struct appdata
                {
                    float4 vertex : POSITION;
                    float2 uv0 : TEXCOORD0;
                    float4 normal : NORMAL;
                    float4 tangent : TANGENT;
                };

                struct v2f
                {
                    float4 pos : SV_POSITION;
                    float2 uv0 : TEXCOORD0;
                    float4 worldPos : TEXCOORD1;
                    float3 worldNormal : TEXCOORD2;
                    float3 worldTangent : TEXCOORD3;
                    float3 worldBiTangent : TEXCOORD4;
                    LIGHTING_COORDS(5, 6)
                };

                v2f vert(appdata v)
                {
                    v2f o = (v2f)0;
                    o.pos = UnityObjectToClipPos(v.vertex);
                    o.uv0 = v.uv0;
                    o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                    o.worldNormal = UnityObjectToWorldNormal(v.normal);
                    o.worldTangent = normalize(mul(unity_ObjectToWorld, float4(v.tangent.xyz, 0.0)).xyz);
                    o.worldBiTangent = normalize(cross(o.worldNormal, o.worldTangent) * v.tangent.w);
                    TRANSFER_VERTEX_TO_FRAGMENT(o)
                    return o;
                }

                float4 frag(v2f i) : COLOR
                {
                    //ready for vector
                    float3 nDirTS = UnpackNormal(tex2D(_NormTex, i.uv0)).rgb;
                    float3x3 TBN = float3x3(i.worldTangent, i.worldBiTangent, i.worldNormal);
                    float3 nDirWS = normalize(mul(nDirTS, TBN));
                    float3 vDirWS = normalize(_WorldSpaceCameraPos.xyz - i.worldPos.xyz);
                    float3 vrDirWS = reflect(-vDirWS, nDirWS);
                    float3 lDirWS = _WorldSpaceLightPos0.xyz;
                    float3 lrDirWS = reflect(-lDirWS, nDirWS);
                    //Ready for dot Result
                    float ndotl = dot(nDirWS, lDirWS);
                    float vdotr = dot(vDirWS, lrDirWS);
                    float vdotn = dot(vDirWS, nDirWS);
                    //texture 
                    float4 var_MainTex = tex2D(_MainTex, i.uv0);
                    float4 var_SpecTex = tex2D(_SpecTex, i.uv0);
                    float3 var_EmitTex = tex2D(_EmitTex, i.uv0).rgb;
                    float3 var_CubeMap = tex2D(_CubeMap, float4(vrDirWS, lerp(_CubeMapMip, 0.0, var_SpecTex.a))).rgb;
                    //directional lighting
                    float3 baseCol = var_MainTex.rgb * _MainCol;
                    float lambert = max(0.0, ndotl);
                    float specCol = var_SpecTex.rgb;
                    float specPow = lerp(1, _SpecPow, var_SpecTex.a);
                    float phong = pow(max(0.0, vdotr), specPow);
                    float shadow = LIGHT_ATTENUATION(i);
                    float3 dirLighting = (baseCol * lambert + specCol * phong) * _LightColor0 * shadow;
                    //ambient lighting
                    float upMask = max(0, nDirWS.g);
                    float downMask = max(0, -nDirWS.g);
                    float sideMask = 1.0 - upMask - downMask;

                    float envCol = _EnvUpCol * upMask + _EnvSideCol * sideMask + _EnvDownCol * downMask;
                    float fresnel = pow(max(0.0, 1.0 - vdotn), _FresnelPow);
                    float occlusion = var_MainTex.a;
                    float3 envLighting = (baseCol * envCol * _EnvDiffInt + var_CubeMap * fresnel * _EnvSpecInt * var_SpecTex.a) * occlusion;

                    //emission lighitng
                    float3 emission = var_EmitTex * _EmitInt;


                    float3 finalRGB = dirLighting + envLighting + emission;
                    return float4 (finalRGB, 1.0);
                }
                ENDCG
            }
        }
            FallBack"Diffuse"
}
